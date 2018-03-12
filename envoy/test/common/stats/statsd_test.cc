#include <chrono>
#include <memory>

#include "common/network/utility.h"
#include "common/stats/statsd.h"
#include "common/upstream/upstream_impl.h"

#include "test/common/upstream/utility.h"
#include "test/mocks/buffer/mocks.h"
#include "test/mocks/local_info/mocks.h"
#include "test/mocks/network/mocks.h"
#include "test/mocks/stats/mocks.h"
#include "test/mocks/thread_local/mocks.h"
#include "test/mocks/upstream/mocks.h"

#include "gmock/gmock.h"
#include "gtest/gtest.h"

using testing::InSequence;
using testing::Invoke;
using testing::NiceMock;
using testing::Return;
using testing::_;

namespace Envoy {
namespace Stats {
namespace Statsd {

class TcpStatsdSinkTest : public testing::Test {
public:
  TcpStatsdSinkTest() {
    sink_.reset(
        new TcpStatsdSink(local_info_, "fake_cluster", tls_, cluster_manager_,
                          cluster_manager_.thread_local_cluster_.cluster_.info_->stats_store_));
  }

  void expectCreateConnection() {
    connection_ = new NiceMock<Network::MockClientConnection>();
    Upstream::MockHost::MockCreateConnectionData conn_info;
    conn_info.connection_ = connection_;
    conn_info.host_description_ = Upstream::makeTestHost(
        Upstream::ClusterInfoConstSharedPtr{new Upstream::MockClusterInfo}, "tcp://127.0.0.1:80");

    EXPECT_CALL(cluster_manager_, tcpConnForCluster_("fake_cluster", _))
        .WillOnce(Return(conn_info));
    EXPECT_CALL(*connection_, setConnectionStats(_));
    EXPECT_CALL(*connection_, connect());
  }

  NiceMock<ThreadLocal::MockInstance> tls_;
  NiceMock<Upstream::MockClusterManager> cluster_manager_;
  std::unique_ptr<TcpStatsdSink> sink_;
  NiceMock<LocalInfo::MockLocalInfo> local_info_;
  Network::MockClientConnection* connection_{};
};

TEST_F(TcpStatsdSinkTest, EmptyFlush) {
  InSequence s;

  sink_->beginFlush();
  expectCreateConnection();
  EXPECT_CALL(*connection_, write(BufferStringEqual(""), _));
  sink_->endFlush();
}

TEST_F(TcpStatsdSinkTest, BasicFlow) {
  InSequence s;
  NiceMock<MockCounter> counter;
  counter.name_ = "test_counter";

  NiceMock<MockGauge> gauge;
  gauge.name_ = "test_gauge";

  sink_->beginFlush();
  sink_->flushCounter(counter, 1);
  sink_->flushGauge(gauge, 2);

  expectCreateConnection();
  EXPECT_CALL(*connection_,
              write(BufferStringEqual("envoy.test_counter:1|c\nenvoy.test_gauge:2|g\n"), _));
  sink_->endFlush();

  connection_->runHighWatermarkCallbacks();
  connection_->runLowWatermarkCallbacks();

  // Test a disconnect. We should connect again.
  connection_->raiseEvent(Network::ConnectionEvent::RemoteClose);

  expectCreateConnection();

  NiceMock<MockHistogram> timer;
  timer.name_ = "test_timer";
  EXPECT_CALL(*connection_, write(BufferStringEqual("envoy.test_timer:5|ms\n"), _));
  sink_->onHistogramComplete(timer, 5);

  EXPECT_CALL(*connection_, close(Network::ConnectionCloseType::NoFlush));
  tls_.shutdownThread();
}

TEST_F(TcpStatsdSinkTest, BufferReallocate) {
  InSequence s;

  NiceMock<MockCounter> counter;
  counter.name_ = "test_counter";

  sink_->beginFlush();
  for (int i = 0; i < 2000; i++) {
    sink_->flushCounter(counter, 1);
  }

  expectCreateConnection();
  EXPECT_CALL(*connection_, write(_, _))
      .WillOnce(Invoke([](Buffer::Instance& buffer, bool) -> void {
        std::string compare;
        for (int i = 0; i < 2000; i++) {
          compare += "envoy.test_counter:1|c\n";
        }
        EXPECT_EQ(compare, TestUtility::bufferToString(buffer));
      }));
  sink_->endFlush();
}

TEST_F(TcpStatsdSinkTest, Overflow) {
  InSequence s;

  NiceMock<MockCounter> counter;
  counter.name_ = "test_counter";

  // Synthetically set buffer above high watermark. Make sure we don't write anything.
  cluster_manager_.thread_local_cluster_.cluster_.info_->stats().upstream_cx_tx_bytes_buffered_.set(
      1024 * 1024 * 17);
  sink_->beginFlush();
  sink_->flushCounter(counter, 1);
  sink_->endFlush();

  // Lower and make sure we write.
  cluster_manager_.thread_local_cluster_.cluster_.info_->stats().upstream_cx_tx_bytes_buffered_.set(
      1024 * 1024 * 15);
  sink_->beginFlush();
  sink_->flushCounter(counter, 1);
  expectCreateConnection();
  EXPECT_CALL(*connection_, write(BufferStringEqual("envoy.test_counter:1|c\n"), _));
  sink_->endFlush();

  // Raise and make sure we don't write and kill connection.
  cluster_manager_.thread_local_cluster_.cluster_.info_->stats().upstream_cx_tx_bytes_buffered_.set(
      1024 * 1024 * 17);
  sink_->beginFlush();
  sink_->flushCounter(counter, 1);
  EXPECT_CALL(*connection_, close(Network::ConnectionCloseType::NoFlush));
  sink_->endFlush();

  EXPECT_EQ(2UL, cluster_manager_.thread_local_cluster_.cluster_.info_->stats_store_
                     .counter("statsd.cx_overflow")
                     .value());
  tls_.shutdownThread();
}

} // namespace Statsd
} // namespace Stats
} // namespace Envoy

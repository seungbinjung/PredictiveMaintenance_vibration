import LiveChart from "../components/LiveChart";
import ProbabilityGauge from "../components/ProbabilityGauge";
import StatusIndicator from "../components/StatusIndicator";
import RecentEvents from "../components/RecentEvents";

export default function Dashboard() {
  return (
    <div className="grid grid-cols-3 gap-6">
      <div className="col-span-2 bg-[#1a1a1a] p-4 rounded-xl shadow-xl border border-gray-700">
        <h2 className="text-xl mb-4 text-green-400 font-bold">
          🔧 실시간 진동 데이터
        </h2>
        <LiveChart />
      </div>

      <div className="bg-[#1a1a1a] p-4 rounded-xl shadow-xl border border-gray-700">
        <h2 className="text-xl mb-4 text-green-400 font-bold">
          📊 예측 확률
        </h2>
        <ProbabilityGauge />
      </div>

      <div className="col-span-2 bg-[#1a1a1a] p-4 rounded-xl mt-6 shadow-xl border border-gray-700">
        <h2 className="text-xl mb-4 text-yellow-300 font-bold">
          ⚠️ 전동기 설비 상태
        </h2>
        <RecentEvents />
      </div>

      <div className="bg-[#1a1a1a] p-4 rounded-xl mt-6 shadow-xl border border-gray-700">
        <h2 className="text-xl mb-4 text-blue-300 font-bold">
          🖥 시스템 연결 상태
        </h2>
        <StatusIndicator />
      </div>
    </div>
  );
}

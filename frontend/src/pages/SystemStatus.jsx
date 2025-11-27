import StatusIndicator from "../components/StatusIndicator";

export default function SystemStatus() {
  return (
    <div className="bg-[#1a1a1a] p-6 rounded-xl shadow-xl border border-gray-700">
      <h2 className="text-xl text-blue-300 font-bold mb-4">
        🖥 시스템 상태 정보
      </h2>
      <StatusIndicator />
    </div>
  );
}

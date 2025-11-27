import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavigationSidebar from "./components/NavigationSidebar";
import Dashboard from "./pages/Dashboard";
import Events from "./pages/Events";
import SystemStatus from "./pages/SystemStatus";

export default function App() {
  return (
    <Router>
      <div className="flex bg-[#0e0e0e] min-h-screen text-gray-200">
        <NavigationSidebar />

        <div className="flex-1 p-6 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/events" element={<Events />} />
            <Route path="/system" element={<SystemStatus />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

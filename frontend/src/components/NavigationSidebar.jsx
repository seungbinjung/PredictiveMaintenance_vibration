import { Link, useLocation } from "react-router-dom";

export default function NavigationSidebar() {
  const location = useLocation();

  const menu = [
    { name: "Dashboard", path: "/" },
    { name: "Events", path: "/events" },
    { name: "System Status", path: "/system" },
  ];

  return (
    <div className="w-64 bg-[#1a1a1a] p-6 border-r border-gray-700">
      <h1 className="text-xl font-bold mb-8 text-green-400">
        🏭 Vibration Monitor
      </h1>

      <ul className="space-y-4">
        {menu.map((item) => (
          <li key={item.path}>
            <Link
              to={item.path}
              className={`block px-4 py-2 rounded-lg text-lg 
                ${
                  location.pathname === item.path
                    ? "bg-green-600 text-white"
                    : "hover:bg-[#222] text-gray-300"
                }`}
            >
              {item.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

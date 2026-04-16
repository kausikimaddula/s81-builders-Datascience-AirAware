import { Navigate, Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar";
import DashboardPage from "./pages/DashboardPage";
import DataTablePage from "./pages/DataTablePage";
import SmartAILabPage from "./pages/SmartAILabPage";
import UploadPage from "./pages/UploadPage";

function App() {
  return (
    <div className="min-h-screen">
      <NavBar />
      <main className="mx-auto w-full max-w-6xl px-4 py-6 md:px-6 md:py-8">
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/ai-lab" element={<SmartAILabPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/data-table" element={<DataTablePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

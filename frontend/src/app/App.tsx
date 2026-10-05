import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "../components/layout/AppShell";
import { DashboardPage } from "../pages/DashboardPage";
import { DocumentsPage } from "../pages/DocumentsPage";
import { DocumentWorkspacePage } from "../pages/DocumentWorkspacePage";
import { JobPage } from "../pages/JobPage";
import { SettingsPage } from "../pages/SettingsPage";

export function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/documents" element={<DocumentsPage />} />
        <Route path="/documents/:documentId" element={<DocumentWorkspacePage />} />
        <Route path="/jobs" element={<JobPage />} />
        <Route path="/jobs/:jobId" element={<JobPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Route>
    </Routes>
  );
}

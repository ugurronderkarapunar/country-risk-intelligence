import { Route, Routes } from "react-router-dom";
import { Dashboard } from "./pages/Dashboard";
import { CountryPage } from "./pages/CountryPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/country/:iso2" element={<CountryPage />} />
    </Routes>
  );
}

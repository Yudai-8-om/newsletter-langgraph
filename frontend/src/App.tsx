import { Routes, Route } from "react-router";
import "./App.css";
import LandingPage from "./components/LandingPage";

function App() {
  return (
    <>
      <div className="min-h-screen">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          {/* <Route
            path="/search"
            element={
              <MetricsPage
                ticker={ticker}
                metrics={metrics}
                loading={loading}
                error={error}
              />
            }
          /> */}
        </Routes>
      </div>
    </>
  );
}

export default App;

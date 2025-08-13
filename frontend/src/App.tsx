import { Routes, Route } from "react-router";
import "./App.css";
import LandingPage from "./components/LandingPage";
import Dashboard from "./components/Dashboard";
import PrivateRoute from "./components/PrivateRoute";
import SubscriptionSuccess from "./components/SubscriptionSuccess";
import SubscriptionFailure from "./components/SubscriptionFailure";
import AccountInfo from "./components/AccountInfo";

function App() {
  return (
    <>
      <div className="min-h-screen">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/account"
            element={
              <PrivateRoute>
                <AccountInfo />
              </PrivateRoute>
            }
          />
          <Route
            path="/subscription/success"
            element={<SubscriptionSuccess />}
          />
          <Route
            path="/subscription/failure"
            element={<SubscriptionFailure />}
          />
        </Routes>
      </div>
    </>
  );
}

export default App;

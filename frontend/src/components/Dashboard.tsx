import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import type { Newsletter } from "../api/NewsletterAPI";
import {
  getNewsletters,
  getMyInfo,
  postUpgradeRequest,
} from "../api/NewsletterAPI";
import { useAuth } from "../hooks/useAuth";

const Dashboard = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [newsletters, setNewsletters] = useState<Newsletter[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isSubscribed, setIsSubscribed] = useState<boolean | null>(null);

  useEffect(() => {
    const checkSubscription = async () => {
      try {
        const status = await getMyInfo();
        setIsSubscribed(status.is_subscribed);
      } catch (error) {
        console.error("Failed to fetch status:", error);
        setIsSubscribed(false);
      }
    };
    const fetchNewsletters = async () => {
      try {
        const newsletters = await getNewsletters();
        setNewsletters(newsletters);
      } catch (error) {
        console.error("Failed to fetch newsletters:", error);
      }
    };
    checkSubscription();
    fetchNewsletters();
  }, []);

  const handleUpgradeRequest = async () => {
    try {
      const stripeUrl = await postUpgradeRequest();
      window.open(stripeUrl.checkout_url, "_blank");
    } catch (error) {
      console.error("Failed to create upgrade session:", error);
      alert("Failed to create upgrade session. Please contact support team.");
    }
  };

  const handleLogout = async () => {
    logout();
    navigate("/");
    alert("You successfully logged out.");
  };

  const handleAccountInfoRequest = () => {
    navigate("/account");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Newsletter Dashboard
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              {!isSubscribed && (
                <button
                  onClick={handleUpgradeRequest}
                  className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition"
                >
                  Upgrade to Premium
                </button>
              )}

              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-md text-sm font-medium"
              >
                Logout
              </button>
              <button
                onClick={handleAccountInfoRequest}
                className={
                  isSubscribed
                    ? "p-2 text-green-500 hover:text-green-800 hover:bg-gray-100 rounded-full transition-colors"
                    : "p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-full transition-colors"
                }
                aria-label="Account"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-5 sm:p-6">
          {newsletters.length > 0 && (
            <div className="relative">
              <div className="overflow-hidden">
                <div
                  className="flex transition-transform duration-300 ease-in-out"
                  style={{
                    transform: `translateX(-${currentIndex * 100}%)`,
                  }}
                >
                  {newsletters.map((newsletter: Newsletter) => (
                    <div
                      key={newsletter.id}
                      className="w-full flex-shrink-0 px-4"
                    >
                      <div className="bg-white rounded-xl shadow-md border border-gray-100 max-w-4xl mx-auto">
                        <div className="bg-gradient-to-r from-blue-500 to-purple-600 h-2"></div>

                        <div className="p-8">
                          <h1 className="text-3xl font-bold text-gray-900 mb-6">
                            {newsletter.title}
                          </h1>

                          <div className="text-gray-700 leading-relaxed text-lg whitespace-pre-wrap">
                            {newsletter.content}
                          </div>

                          <div className="flex items-center justify-between pt-6 mt-6 border-t border-gray-100">
                            <div className="flex items-center text-sm text-gray-500">
                              <svg
                                className="w-4 h-4 mr-1"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth="2"
                                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                                ></path>
                              </svg>
                              {new Date(
                                newsletter.created_at
                              ).toLocaleDateString("en-US", {
                                month: "long",
                                day: "numeric",
                                year: "numeric",
                              })}
                            </div>

                            <div className="text-sm text-gray-500">
                              {currentIndex + 1} of {newsletters.length}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {newsletters.length > 1 && (
                <div>
                  <button
                    onClick={() =>
                      setCurrentIndex((prev) =>
                        prev > 0 ? prev - 1 : newsletters.length - 1
                      )
                    }
                    className="absolute left-2 top-1/2 -translate-y-1/2 bg-white hover:bg-gray-50 shadow-lg rounded-full p-3 transition-colors border border-gray-200"
                  >
                    <svg
                      className="w-6 h-6 text-gray-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M15 19l-7-7 7-7"
                      ></path>
                    </svg>
                  </button>

                  <button
                    onClick={() =>
                      setCurrentIndex((prev) =>
                        prev < newsletters.length - 1 ? prev + 1 : 0
                      )
                    }
                    className="absolute right-2 top-1/2 -translate-y-1/2 bg-white hover:bg-gray-50 shadow-lg rounded-full p-3 transition-colors border border-gray-200"
                  >
                    <svg
                      className="w-6 h-6 text-gray-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M9 5l7 7-7 7"
                      ></path>
                    </svg>
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

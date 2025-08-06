import { useState } from "react";
import { Mail, Calendar, TrendingUp } from "lucide-react";
import AuthCard from "./AuthCard";
import NewsletterArticle from "./NewsLetterArticle";

const LandingPage = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 w-screen">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center max-w-screen-xl">
            <div className="flex items-center p-4">
              <TrendingUp className="h-8 w-8 mr-2 text-blue-700" />
              <span className="lg:text-2xl text-xl font-bold text-gray-900">
                BUZZ
              </span>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => {
                  setShowLogin(true);
                  setShowRegister(false);
                }}
                className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-xl font-medium hover:bg-gray-50 bg-blue"
              >
                Sign In
              </button>
              <button
                onClick={() => {
                  setShowRegister(true);
                  setShowLogin(false);
                }}
                className="bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-medium hover:bg-blue-700 transition"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Stay Informed with AI-Curated News
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Get the most important trending news delivered to your inbox daily,
            curated and summarized by artificial intelligence.
          </p>

          <div className="flex justify-center space-x-4 mb-12">
            <div className="flex items-center text-gray-600">
              <Mail className="h-5 w-5 mr-2" />
              Daily delivery
            </div>
            <div className="flex items-center text-gray-600">
              <TrendingUp className="h-5 w-5 mr-2" />
              AI-curated content
            </div>
            <div className="flex items-center text-gray-600">
              <Calendar className="h-5 w-5 mr-2" />
              Always up-to-date
            </div>
          </div>
        </div>

        <NewsletterArticle />

        <div className="text-center bg-blue-600 rounded-lg p-12 text-white">
          <h3 className="text-3xl font-bold mb-4">Ready to Stay Informed?</h3>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of readers who trust our AI to keep them updated
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <div className="text-lg">
              <span className="font-semibold">Free tier available</span> •
              $1/month for premium
            </div>
          </div>
          <button
            onClick={() => setShowRegister(true)}
            className="mt-6 bg-white text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-100 transition duration-200"
          >
            Start Reading Today
          </button>
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>&copy; 2025 AI Newsletter. Stay informed, stay ahead.</p>
          </div>
        </div>
      </footer>

      {showLogin && (
        <AuthCard isLogin={true} onClose={() => setShowLogin(false)} />
      )}
      {showRegister && (
        <AuthCard isLogin={false} onClose={() => setShowRegister(false)} />
      )}
    </div>
  );
};
export default LandingPage;

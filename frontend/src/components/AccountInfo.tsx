import { useEffect, useState } from "react";
import { deleteUser, getMyInfo } from "../api/NewsletterAPI";
import { useNavigate } from "react-router";

const AccountInfo = () => {
  const navigate = useNavigate();
  const [isSubscribed, setIsSubscribed] = useState<boolean | null>(null);
  const [email, setEmail] = useState<string | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [password, setPassword] = useState("");
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const checkAccount = async () => {
      try {
        const status = await getMyInfo();
        setEmail(status.email);
        setIsSubscribed(status.is_subscribed);
      } catch (error) {
        console.error("Failed to fetch status:", error);
        setIsSubscribed(false);
      }
    };

    checkAccount();
  }, []);

  const handleBack = () => {
    navigate("/dashboard");
  };

  const handleDeleteClick = () => {
    setShowDeleteModal(true);
    setPassword("");
    setShowConfirmation(false);
  };

  const handlePasswordSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password.trim()) {
      setShowConfirmation(true);
    }
  };

  const handleCancelDelete = () => {
    setShowConfirmation(false);
  };
  const handleConfirmDelete = async () => {
    if (!email) return;

    setIsDeleting(true);
    try {
      await deleteUser({
        email: email,
        password: password,
      });
      alert("Account deleted successfully");
      navigate("/");
    } catch (error) {
      console.error("Failed to delete account:", error);
      alert(
        "Failed to delete account. Please check your password and try again."
      );
    } finally {
      setIsDeleting(false);
      setShowDeleteModal(false);
      setPassword("");
      setShowConfirmation(false);
    }
  };

  const handleModalClose = () => {
    setShowDeleteModal(false);
    setPassword("");
    setShowConfirmation(false);
  };

  return (
    <>
      <div className="bg-white overflow-hidden shadow rounded-lg mb-6">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Account Information
          </h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <div className="text-sm font-medium text-gray-500">Email</div>
              <div className="mt-1 text-sm text-gray-900">{email}</div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-500">
                Subscription
              </div>
              <div className="mt-1">
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    isSubscribed
                      ? "bg-green-100 text-green-800"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {isSubscribed ? "Premium Version" : "Free Version"}
                </span>
              </div>
            </div>
            <div className="mt-8 pt-6 border-t border-gray-200">
              <button
                onClick={handleBack}
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md text-sm transition-colors mb-6"
              >
                Back to Dashboard
              </button>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-gray-200">
            <h4 className="text-md font-medium text-gray-900 mb-2">
              Danger Zone
            </h4>
            <p className="text-sm text-gray-600 mb-4">
              Once you delete your account, there is no going back. Please be
              certain.
            </p>
            <button
              onClick={handleDeleteClick}
              className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md text-sm transition-colors"
            >
              Delete Account
            </button>
          </div>
        </div>
      </div>

      {showDeleteModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              {!showConfirmation ? (
                <>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Delete Account
                  </h3>
                  <p className="text-sm text-gray-600 mb-4">
                    Please enter your password to confirm account deletion.
                  </p>
                  <form onSubmit={handlePasswordSubmit}>
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter your password"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500"
                      required
                      autoFocus
                    />
                    <div className="mt-4 flex justify-end space-x-3">
                      <button
                        type="button"
                        onClick={handleModalClose}
                        className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition-colors"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
                      >
                        Continue
                      </button>
                    </div>
                  </form>
                </>
              ) : (
                <>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Confirm Account Deletion
                  </h3>
                  <p className="text-sm text-gray-600 mb-4">
                    Are you sure you want to delete your account? This action
                    will:
                  </p>
                  <ul className="text-sm text-gray-600 mb-4 list-disc list-inside space-y-1">
                    <li>Permanently delete your account</li>
                    {isSubscribed && <li>Cancel your subscription</li>}
                    <li>Remove all your data</li>
                  </ul>
                  <p className="text-sm font-medium text-red-600 mb-4">
                    This action cannot be undone.
                  </p>
                  <div className="flex justify-end space-x-3">
                    <button
                      onClick={handleCancelDelete}
                      disabled={isDeleting}
                      className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition-colors disabled:opacity-50"
                    >
                      Back
                    </button>
                    <button
                      onClick={handleConfirmDelete}
                      disabled={isDeleting}
                      className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center"
                    >
                      {isDeleting ? (
                        <>
                          <svg
                            className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                          >
                            <circle
                              className="opacity-25"
                              cx="12"
                              cy="12"
                              r="10"
                              stroke="currentColor"
                              strokeWidth="4"
                            ></circle>
                            <path
                              className="opacity-75"
                              fill="currentColor"
                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            ></path>
                          </svg>
                          Deleting...
                        </>
                      ) : (
                        "Delete Account"
                      )}
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default AccountInfo;

const AccountInfo = () => {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg mb-6">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
          Account Information
        </h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">Email</dt>
            <dd className="mt-1 text-sm text-gray-900">user.email</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Subscription</dt>
            <dd className="mt-1">
              <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                paid
                {/* ${
                      user?.subscription_status === "paid"
                        ? "bg-green-100 text-green-800"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {user?.subscription_status === "paid" ? "Premium" : "Free"} */}
              </span>
            </dd>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccountInfo;

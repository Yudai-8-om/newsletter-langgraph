const baseUrl = import.meta.env.VITE_BACKEND_URL;

export interface Newsletter {
  id: number;
  title: string;
  content: string;
  created_at: string;
}

export interface UserRequest {
  email: string;
  password: string;
}

export interface UserSubscriptionStatus {
  email: string;
  is_subscribed: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface StripeUrl {
  checkout_url: string;
}

export interface GeneralResponse {
  detail: string;
}

async function get<T>(url: string, token: string | null): Promise<T> {
  const headers = new Headers();
  headers.append("Content-Type", "application/json");
  if (token) {
    headers.append("Authorization", `Bearer ${token}`);
  }
  const response = await fetch(url, {
    method: "GET",
    headers,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Status: ${response.status}, Message: ${errorText}`);
  }
  return response.json();
}

export async function getNewsletters(): Promise<Newsletter[]> {
  const url = `${baseUrl}/newsletters`;
  const token = sessionStorage.getItem("session_token");
  try {
    const newsletters = await get<Newsletter[]>(url, token);
    return newsletters;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to fetch newsletters: ${error.message}`);
    } else {
      throw new Error("An unknown error occurred while fetching newsletters");
    }
  }
}

export async function getMyInfo(): Promise<UserSubscriptionStatus> {
  const url = `${baseUrl}/me`;
  const token = sessionStorage.getItem("session_token");
  try {
    const status = await get<UserSubscriptionStatus>(url, token);
    return status;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to fetch user info: ${error.message}`);
    } else {
      throw new Error("An unknown error occurred while fetching user info");
    }
  }
}

async function post<T>(
  url: string,
  data: any,
  token?: string | null
): Promise<T> {
  const headers = new Headers();
  headers.append("Content-Type", "application/json");
  if (token) {
    headers.append("Authorization", `Bearer ${token}`);
  }
  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Status: ${response.status}, Message: ${errorText}`);
  }
  return response.json();
}

export async function postLoginRequest(user: UserRequest): Promise<Token> {
  const url = `${baseUrl}/login`;
  try {
    const sessionToken = await post<Token>(url, user);
    return sessionToken;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to login: ${error.message}`);
    } else {
      throw new Error("An unknown error occurred while requesting login");
    }
  }
}

export async function postRegisterRequest(user: UserRequest): Promise<Token> {
  const url = `${baseUrl}/register`;
  try {
    const sessionToken = await post<Token>(url, user);
    return sessionToken;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to register: ${error.message}`);
    } else {
      throw new Error("An unknown error occurred while requesting register");
    }
  }
}

export async function postUpgradeRequest() {
  const url = `${baseUrl}/subscription`;
  const token = sessionStorage.getItem("session_token");
  try {
    const stripeUrl = await post<StripeUrl>(
      url,
      { subscription: "activate" },
      token
    );
    return stripeUrl;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed: ${error.message}`);
    } else {
      throw new Error("An unknown error occurred while requesting upgrade");
    }
  }
}

async function deleteMethod<T>(
  url: string,
  data: any,
  token: string | null
): Promise<T> {
  const headers = new Headers();
  headers.append("Content-Type", "application/json");
  headers.append("Authorization", `Bearer ${token}`);
  const response = await fetch(url, {
    method: "DELETE",
    headers,
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Status: ${response.status}, Message: ${errorText}`);
  }
  return response.json();
}

export async function deleteUser(user: UserRequest) {
  const url = `${baseUrl}/user`;
  const token = sessionStorage.getItem("session_token");
  try {
    const result = await deleteMethod<GeneralResponse>(url, user, token);
    return result;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed: ${error.message}`);
    } else {
      throw new Error("An unknown error occurred while requesting upgrade");
    }
  }
}

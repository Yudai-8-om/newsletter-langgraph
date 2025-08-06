import dotenv from "dotenv";

// dotenv.config({ path: "../../../.env" });
// const baseURL = process.env.BASE_URL;
const baseURL = "http://localhost:8000";

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

export interface Token {
  access_token: string;
  token_type: string;
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

async function post<T>(url: string, data: any, token?: string): Promise<T> {
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

export async function getNewsletters(): Promise<Newsletter[]> {
  const url = `${baseURL}/newsletters`;
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

export async function postLoginRequest(user: UserRequest): Promise<Token> {
  const url = `${baseURL}/login`;
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
  const url = `${baseURL}/register`;
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

"use client";

import { useState } from "react";
import { authApi } from "@/lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function submit() {
    const response = await authApi.login(email, password);
    localStorage.setItem("token", response.data.data.access_token);
    window.location.href = "/dashboard";
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center p-6">
      <div className="panel p-6">
        <h1 className="mb-4 text-2xl font-semibold">Sign in</h1>
        <input className="mb-3 w-full rounded-md border p-2" placeholder="Email" value={email} onChange={(event) => setEmail(event.target.value)} />
        <input className="mb-4 w-full rounded-md border p-2" placeholder="Password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
        <button className="w-full rounded-md bg-brand px-4 py-2 text-white" onClick={submit}>Login</button>
      </div>
    </main>
  );
}

"use server";

import { revalidatePath } from "next/cache";
import { cookies } from "next/headers";
import { isLocale, localeCookie } from "@/i18n/config";

export async function setLocale(value: string): Promise<void> {
  if (!isLocale(value)) return; // never trust input
  (await cookies()).set(localeCookie, value, {
    path: "/",
    maxAge: 60 * 60 * 24 * 365,
    sameSite: "lax",
  });
  revalidatePath("/", "layout");
}
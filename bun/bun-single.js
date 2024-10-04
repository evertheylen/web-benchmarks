import { serve } from "bun";
import { getUsers } from "./common.js";

async function handler(req) {
  try {
    const users = await getUsers();
    return new Response(JSON.stringify(users), { status: 200, headers: { "Content-Type": "application/json" } });
  } catch (e) {
    console.error(e);
    return new Response(null, { status: 500 });
  }
}

serve({
  fetch: handler,
  port: 8000,
  development: false,
  // like cluster
  reusePort: true,
});

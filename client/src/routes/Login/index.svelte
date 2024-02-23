<script>
  import { onMount, getContext } from "svelte";
  import { currentUser, authToken, server } from "../../stores/stores.js";
  import { navigate } from "svelte-routing"; // Assuming you're using svelte-routing for navigation

  let email = "";
  let password = "";
  let errorMessage = ""; // To display login errors

  let isAuthenticated = false;

  onMount(() => {
    isAuthenticated = $authToken !== "";
    console.log(isAuthenticated);
    if (isAuthenticated) {
      navigate("/home");
    }
  });

  async function handleLogin() {
    const loginEndpoint = server + "/api/token/";
    console.log(loginEndpoint);
    const credentials = { email, password };

    try {
      const response = await fetch(loginEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        throw new Error("Login failed"); // Handle non-2xx responses
      }

      const data = await response.json();
      authToken.update((value) => value = data.access);
      currentUser.set({
          userId: data.id,
          name: data.name,
          email: data.email,
          github: data.github
      });
      
      navigate("/home");
    } catch (error) {
      errorMessage = error.message;
    }
  }
</script>

<div class="login-container">
  {#if errorMessage}
    <p class="error-message">{errorMessage}</p>
  {/if}
  <h1 class="text-[5em] font-bold text-[teal]">NexaPulse</h1>
  <form class="login-form" on:submit|preventDefault={handleLogin}>
    <input
      type="email"
      class="login-input"
      placeholder="Email"
      bind:value={email}
      required
    />
    <input
      type="password"
      class="login-input"
      placeholder="Password"
      bind:value={password}
      required
    />
    <button type="submit" class="login-button">Login</button>
  </form>
</div>

<style>
  @import "style.css";
</style>

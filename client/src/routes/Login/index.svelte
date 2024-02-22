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
      $authToken = data.access; // Assuming the Django backend uses a 'access' token
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
  .login-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #e0f2f1; /* Light teal background */
    color: black;
  }

  .login-form {
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background: #ffffff;
    width: 100%;
    max-width: 30%;
  }

  .login-input {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    border: 1px solid #b2dfdb; /* Teal border */
    border-radius: 0.25rem;
    box-sizing: border-box;
  }

  .login-button {
    width: 100%;
    padding: 0.75rem;
    border: none;
    border-radius: 0.25rem;
    background-color: #009688; /* Teal background */
    color: white;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: background-color 0.3s;
  }

  .login-button:hover {
    background-color: #00796b; /* Darker teal for hover */
  }
</style>

<script>
  import { onMount, getContext } from "svelte";
  import {
    currentUser,
    authToken,
    refreshToken,
    server,
  } from "../../stores/stores.js";
  import { navigate } from "svelte-routing"; // Assuming you're using svelte-routing for navigation

  let email = "";
  let password = "";
  let displayName = "";
  let github = "";
  let errorMessage = ""; // To display login errors
  let isLoggingIn = true; // Track whether the user is logging in or signing up

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
      authToken.update((value) => (value = data.access));
      refreshToken.update((value) => (value = data.refresh));

      console.log("data:", data)
      if (!data.is_active) {
        throw new Error("User not activated"); // Handle non-2xx responses
      }
      currentUser.set({
        userId: data.id,
        name: data.name,
        email: data.email,
        github: data.github,
        lastUpdated: data.lastUpdated,
      });
      console.log("DATA ACCESS: " + data.access);
      navigate("/home");
    } catch (error) {
      errorMessage = error.message;
    }
  }

  async function handleSignUp() {
    // Handle sign-up logic here
    const signUpEndpoint = server + "/api/authors/new/";
    console.log(signUpEndpoint);
    const credentials = { 
      "id": null,
      "email":email,
      "password": password,
      "displayName": displayName,
      "github": github
    };
    console.log(credentials);
    try {
      const response = await fetch(signUpEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        throw new Error("Sign up failed"); // Handle non-2xx responses
      }
      const data = await response.json();
      // toggle form to login
      toggleForm();
    } catch (error) {
      errorMessage = error.message;
    }

  }

  function toggleForm() {
    isLoggingIn = !isLoggingIn;
    email = ""; // Reset email and password fields when switching between forms
    password = "";
    errorMessage = ""; // Clear any previous error messages
  }
</script>

<div class="login-container">
  {#if errorMessage}
    <p class="error-message">{errorMessage}</p>
  {/if}
  <h1 class="text-[5em] font-bold text-[teal]">NexaPulse</h1>
  {#if isLoggingIn}
    <!-- Login form -->
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
      <!-- add spacing -->
      <div class="h-4"></div>
      <button class="login-button" on:click={toggleForm}>Sign up</button>
    </form>
  {:else}
    <!-- Sign-up form -->
    <form class="login-form" on:submit|preventDefault={handleSignUp}>
      <input type="text" class="login-input" placeholder="Display Name" bind:value={displayName} required />
      <input type="email" class="login-input" placeholder="Email" bind:value={email} required/>
      <input type="password" class="login-input" placeholder="Password" bind:value={password} required/>
      <input type="url" class="login-input" placeholder="Github" bind:value={github} required/>
      <button type="submit" class="login-button">Sign Up</button>
      <div class="h-4"></div>
      <button class="login-button" on:click={toggleForm}>Back</button>
    </form>
  {/if}
  
</div>

<style>
  @import "style.css";
</style>

<script>
  let email = "";
  let password = "";

  const handleLogin = () => {
    // Logic to handle user login goes here.
    // Typically, you would call an API to authenticate the user.
    console.log("Login attempt:", { email, password });
  };
</script>

<div class="login-container">
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
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #e0f2f1; /* Light teal background */
  }

  .login-form {
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background: #ffffff;
    width: 100%;
    max-width: 320px;
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

<!-- AuthenticatedRoute.svelte -->
<script>
  import { onMount, getContext } from "svelte";
  import { authToken, isLoginPage } from "../stores/stores.js"; // Assuming you have a store for the authentication token
  import { navigate } from "svelte-routing";

  let isAuthenticated = false;

  onMount(() => {
    // Check if the user is authenticated before rendering the route
    isAuthenticated = $authToken !== "";
    console.log(isAuthenticated);
    if (!isAuthenticated) {
      $isLoginPage = true;
      navigate("/"); // Redirect to the login page if not authenticated
    }
  });
</script>

{#if isAuthenticated}
  <!-- Render the protected route if authenticated -->
  <slot />
{/if}

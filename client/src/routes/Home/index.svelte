<script>
  // Data fetching testing
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  // Create a writable store to hold the fetched data
  export let propName = "defaultValue";
  const data = writable([]);

  // Data fetching function
  async function fetchData() {
    const url = "http://127.0.0.1:8000/test"; // Replace with your API endpoint
    const response = await fetch(url);
    const jsonData = await response.json();
    data.set(jsonData);
    console.log(jsonData);
  }

  // Fetch data on component mount
  onMount(() => {
    fetchData().catch(console.error);
  });
</script>

<main>
  <h1>Hello {propName}, this is the home page!</h1>
  <p>This is the response from the server after a GET request: "{$data}"</p>
</main>

<style>
</style>

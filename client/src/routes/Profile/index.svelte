<script>
  export let id;

  import { Link } from "svelte-routing";

  function followButtonClicked(follower) {
    alert(follower + " clicked!");
  }
</script>

<main>
  <h1>Hello, this is the {id} profile page!</h1>
  <h1>
    <button
      class="custom-button"
      on:click={() => followButtonClicked("Scammer")}>follow me</button
    >
  </h1>
  <h2>
    <Link to="/messages/{id}">
      <button class="custom-button">messages</button>
    </Link>
  </h2>
</main>

<style>
  main {
    color: black;
    text-align: center;
  }
  .custom-button {
    text-align: center;
    width: 400px;
    height: 100px;
    font-size: 30px;
  }
</style>

<script>
  export let id;

  import { Link } from "svelte-routing";

  function followButtonClicked(follower) {
    alert(follower + " clicked!");
  }

  let infoDict = {
    "ID": 123312,
    "LOCATION": "Mars, Solar System",
    "FAV GAME": "Dota2, Slay the Spire"
  };
</script>

<main>
  <div class="sidebar"/>
  <div class="navbar"/>
  <div class="main-content">
    <div class="image-container">
      <img src="../../../public/fake_profile.png" alt="used for profile" class="image">
      <div class="circle"/>
    </div>
    <div class="text-container">
      <p class="top-custom-text">Hello, this is the {id} profile page!</p>

      {#each Object.entries(infoDict) as [key, value]}
        <div class="custom-text">{key}: {value}</div>
      {/each}
      
      <div class="button-container">
        <button class="custom-button" on:click={() => followButtonClicked("Scammer")}>follow me</button>
        <Link to="/messages/{id}">
          <button class="custom-button">messages</button>
        </Link>
      </div>
    </div>
  </div>
</main>

<style>
  @import 'profStyle.css';
</style>

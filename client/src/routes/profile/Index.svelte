<script>
  export let id;

  import { Link } from "svelte-routing";

  function followButtonClicked(follower) {
    alert(follower + " clicked!");
  }
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
      <p class="custom-text">Hello, this is the {id} profile page!</p>
      <button class="custom-button" on:click={() => followButtonClicked("Scammer")}>follow me</button>
      <Link to="/messages/{id}">
        <button class="custom-button">messages</button>
      </Link>
    </div>
  </div>
</main>

<style>
  @import 'style.css';
</style>

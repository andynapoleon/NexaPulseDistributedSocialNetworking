<script>
  export let id;

  import { Link } from "svelte-routing";

  function followButtonClicked(follower) {
    alert(follower + " clicked!");
  }
</script>

<main class="container">
  <div class="image-container">
    <!-- Replace 'image-url.jpg' with the URL of your image -->
    <img src="../../../public/fake_profile.png" alt="used for profile" class="image">
  </div>
  <div class="text-container">
    <p class="custom-text">Hello, this is the {id} profile page!</p>
    <button class="custom-button" on:click={() => followButtonClicked("Scammer")}>follow me</button>
    <Link to="/messages/{id}">
      <button class="custom-button">messages</button>
    </Link>
  </div>
</main>

<style>
   .container {
    display: flex;
    align-items: center; /* Vertical alignment */
    justify-content: flex-start; /* Horizontal alignment */
    flex-wrap: wrap; /* Allow items to wrap to the next line if needed */
  }
  
  .image-container {
    position: relative; /* Position the image container relative to the container */
    top: 20%; /* Adjust the top position as needed */
    left: 20%; /* Non-flexible item for the image container */
  }

  .image {
    width: 250px; /* Adjust the width as needed */
    height: auto; /* Maintain aspect ratio */
  }

  .text-container {
    flex: 1 1 auto; /* Flexible item for the text container */
    padding-left: 20px; /* Add space between image and text */
    text-align: center; /* Center text horizontally */
  }

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

  .custom-text {
    font-size: 24px;
    color: rgb(0, 0, 0);
    font-weight: bold;
  }
</style>

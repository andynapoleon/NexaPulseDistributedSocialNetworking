<script>
  export let id;

  let messDict = {
    Scammer: "wants to follow you",
    teacher: "wants to follow you",
  };

  function responseButtonClicked(response) {
    alert(response);
  }
</script>

<main>
  <h1 class="text-black text-center">
    This is the {id}'s personal massage page!
  </h1>
  {#each Object.entries(messDict) as [name, type]}
    <div class="container">
      <div>
        <p class="custom-text">{name} {type}</p>
      </div>
      <div>
        <button
          class="custom-button"
          on:click={() => responseButtonClicked("Yes")}>Yes</button
        >
        <button
          class="custom-button"
          on:click={() => responseButtonClicked("No")}>No</button
        >
      </div>
    </div>
  {/each}
</main>

<style>
  .container {
    border: 2px solid #ccc;
    border-radius: 3%;
    padding: 4%;
    height: 10%;
    width: 70%; /* Increased width to accommodate the text and button */
    display: flex;
    justify-content: space-between; /* Distributes items evenly along the main-axis */
    align-items: center; /* Centers items vertically */
    margin: auto; /* Centers the container horizontally */
    margin-top: 5%;
  }

  .custom-text {
    flex: 1;
    font-size: 24px; /* Set the text size to 16 pixels */
    color: black;
  }

  .custom-button {
    background-color: #007bff;
    color: #fff;
    padding: 8px 24px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
</style>

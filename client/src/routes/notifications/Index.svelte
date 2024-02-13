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

<main {id}>
  {#each Object.entries(messDict) as [name, type]}
    <div class="container">
      <div>
        <p class="custom-text">{name} {type}</p>
      </div>
      <div>
        <button
          class="custom-button-Yes"
          on:click={() => responseButtonClicked("Yes")}
        >
          Yes
        </button>
        <button
          class="custom-button-No"
          on:click={() => responseButtonClicked("No")}
        >
          No
        </button>
      </div>
    </div>
  {/each}
</main>

<style>
  main {
    padding-top: 10%;
    padding-left: 20%;
    padding-right: 7%;
  }

  .container {
    border: 2px solid teal;
    border-radius: 4px; /* Rounded corners */
    padding: 4%;
    height: 50px;
    width: 600px;
    background-color: teal; /* Background color */
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: auto;
    margin-top: 2%;
  }

  .custom-text {
    flex: 5;
    font-size: 24px;
    color: rgb(255, 255, 255);
    font-weight: bold;
  }

  .custom-button-Yes {
    background-color: rgb(52, 197, 255);
    color: rgb(255, 255, 255);
    padding: 4px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }

  .custom-button-No {
    background-color: rgb(190, 0, 0);
    color: rgb(255, 255, 255);
    padding: 4px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }
</style>

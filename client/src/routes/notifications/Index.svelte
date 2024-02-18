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
  <div class="sidebar" />
  <div class="navbar" />
  <div class="main-content">
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
  </div>
</main>

<style>
  @import "notiStyle.css";
</style>

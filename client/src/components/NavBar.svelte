<script>
  import * as Icon from "flowbite-svelte-icons";
  import SearchBar from "./SearchBar.svelte";
  let id = "123"
</script>

<nav>
  <div>
    <img src="../../logo.png" alt="" />
    <h1 class="text-[2em] font-bold text-[#d7efda]">NexaPulse</h1>
  </div>
  <div><SearchBar /></div>
  <div>
    <Icon.BellActiveSolid id="icon" />
    <Icon.MessageCaptionSolid id="icon" />
    <Icon.ArrowUpOutline id="icon" />
    <Icon.UserSettingsSolid id="icon" />
    <div>
      <a href="../profile/{id}">
        <img src="../../fake_profile.png" alt="fake profile" />
      </a>
    </div>
  </div>
</nav>

<style>
  nav {
    position: fixed;
    width: 100%;
    height: 90px; /*Height set to 90px*/
    background-color: teal;
    color: black;
    padding: 1em;
    display: flex;
    justify-content: space-between;
  }

  img {
    width: 3em;
    height: 3em;
  }

  :global(#icon) {
    width: 2em;
    height: 2em;
    color: #e3c4b5;
  }

  div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    column-gap: 1em;
    padding: 0 1em;
  }
</style>

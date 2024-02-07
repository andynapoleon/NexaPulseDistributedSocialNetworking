<script>
  import { Link } from "svelte-routing";
  import * as Icon from "flowbite-svelte-icons";
  import SearchBar from "./SearchBar.svelte";
</script>

<nav>
  <div>
    <img src="../../logo.png" alt="" />
    <h1 class="text-[2em] text-white font-bold text-[#d7efda]">NexaPulse</h1>
  </div>
  <div><SearchBar /></div>
  <div>
    <Icon.BellActiveSolid id="icon" />
    <Icon.MessageCaptionSolid id="icon" />
    <Icon.ArrowUpOutline id="icon" />
    <img src="../../fake_profile.png" alt="fake profile" />
  </div>
</nav>

<style>
  nav {
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

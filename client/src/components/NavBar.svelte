<script>
  import * as Icon from "flowbite-svelte-icons";
  import SearchBar from "./SearchBar.svelte";
  import { currentUser } from "../stores/stores.js";
  import App from "../App.svelte";
  import Counter from "./Counter.svelte";
  import { navigate } from "svelte-routing";

  let id = $currentUser.userId;
  let profileImage = $currentUser.profileImage;

  $: {
    const user = $currentUser;
    id = user.userId;
    profileImage = user.profileImage;
  }

  const navigateProfile = () => {
    navigate(`/profile/${id}`);
    location.reload();
  };
</script>

<nav>
  <div>
    <img src="https://i.ibb.co/yf0RDsB/logo.png" alt="" />
    <h1 class="text-[2em] font-bold text-[#d7efda]">NexaPulse</h1>
  </div>
  <div><SearchBar /></div>
  <div>
    <!--<Icon.BellActiveSolid id="icon" />-->
    <!--<Icon.MessageCaptionSolid id="icon" />-->
    <!--<Icon.ArrowUpOutline id="icon" />-->
    <!--<Icon.UserSettingsSolid id="icon" />-->
    <div>
      <a href={`/profile/${id}`}>
        <button>
          <img class="profile-image" src={profileImage} alt="fake profile" />
        </button>
      </a>
    </div>
  </div>
</nav>

<style>
  nav {
    position: fixed;
    width: 100%;
    background-color: teal;
    color: black;
    padding: 1em;
    display: flex;
    justify-content: space-between;
  }

  img {
    width: 3em;
    height: 3em;
    border-radius: 50%;
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

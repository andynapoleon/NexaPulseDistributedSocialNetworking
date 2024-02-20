<script>
  import { Link } from 'svelte-routing';
  import FriendWidget from "./friendWidget.svelte";

  import { writable } from 'svelte/store';

  let mode = writable(null);

  function switchMode(newMode) {
    mode.set(newMode);
    switch (newMode) {
      case 1:
        currentList = allFriends;
        break;

      case 2:
        currentList = Following;
        break;

      case 3:
        currentList = Follower;
        break;

      default:
        currentList = allFriends;
    }
  }

  let allFriends = [
    {
      id: 1,
      userName: "John Doe",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
    {
      id: 2,
      userName: "HOHO HAHA Doe",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "hoho.haha@example.com",
    },
    {
      id: 3,
      userName: "Bad Apple!",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "bad.apple@example.com",
    },
    {
      id: 4,
      userName: "Number 4",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
    {
      id: 5,
      userName: "Number 5",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
    {
      id: 6,
      userName: "YUUU Doe",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
  ];

  let Following = [
    {
      id: 1,
      userName: "Following 1",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
    {
      id: 2,
      userName: "Following 2",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
    {
      id: 3,
      userName: "Following 3",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
  ];

  let Follower = [
    {
      id: 1,
      userName: "Follower 1",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
    {
      id: 2,
      userName: "Follower 2",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
    {
      id: 3,
      userName: "Follower 3",
      profileImageUrl: "https://i1.sndcdn.com/avatars-000119210476-6i9giz-t500x500.jpg",
      email: "jane.smith@example.com",
    },
  ];

  let currentList = allFriends;
  mode.set(1)
</script>

<main>
  <div class="sidebar"/>
  <div class="navbar"/>
  <div class="main-content">
    <div class="button-layout">
      <button class={$mode === 1 ? 'selected-class-button' : 'class-button'} on:click={() => switchMode(1)}>Friends</button>
      <button class={$mode === 2 ? 'selected-class-button' : 'class-button'} on:click={() => switchMode(2)}>Following</button>
      <button class={$mode === 3 ? 'selected-class-button' : 'class-button'} on:click={() => switchMode(3)}>Follower</button>
    </div>
    {#each Array(Math.ceil(currentList.length/5)) as _, rowIndex}
      <div class="profile-layout">
        {#each Array(Math.min(5, currentList.length - rowIndex * 5)) as _, colIndex}
          <Link to="/profile/{currentList[rowIndex * 5 + colIndex].id}">
            <div class="profile-widget">
              <FriendWidget
                profileImageUrl= {currentList[rowIndex * 5 + colIndex].profileImageUrl}
                name = {currentList[rowIndex * 5 + colIndex].userName}
                email = {currentList[rowIndex * 5 + colIndex].email}
              />
            </div>
          </Link>
        {/each}
      </div>
    {/each}
  </div>
</main>

<style>
  @import "friendStyle.css";
</style>
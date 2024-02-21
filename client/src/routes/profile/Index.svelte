<script>
  import Posts from "../../widgets/Posts.svelte";
  import ProfileWidget from "./ProfileWidget.svelte";
  import { onMount } from "svelte";
  import { authToken, isLoginPage } from "../../stores/stores.js";
  import { navigate } from "svelte-routing"; // Assuming you're using svelte-routing for navigation

  export let id = null;
  let fullName = "";
  let github = "";
  let email = "";

  let isAuthenticated = false;

  onMount(async () => {
    isAuthenticated = $authToken !== "";
    console.log(isAuthenticated);
    if (!isAuthenticated) {
      $isLoginPage = true;
      navigate("/");
    }
    const profileEndpoint = "http://localhost:8000/api/profile/";
    const response = await fetch(profileEndpoint, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${$authToken}`,
      },
    });
    
    if (!response.ok) {
      throw new Error("Failed to fetch profile");
    }
    const data = await response.json();
    fullName = data.full_name;
    github = data.github;
    email = data.email;
  });

  // Fetch names & posts with the userId passed in
  let posts = [
    {
      id: 1,
      userName: "John Doe",
      postTime: "1h ago",
      content: "This is my first post!",
    },
    {
      id: 2,
      userName: "Jane Smith",
      postTime: "2h ago",
      content: "Svelte is awesome!",
    },
    {
      id: 3,
      userName: "Dave Lee",
      postTime: "3h ago",
      content: "Check out my new project.",
    },
  ];
</script>

<main class="main">
  <div class="profile-layout">
    <div class="profile-widget">
      <ProfileWidget
        profileImageUrl="../../../fake_profile.png"
        name={fullName}
        email={email}
        github={github}
        userId={id}
      />
    </div>
    <div class="posts">
      <Posts {posts} />
    </div>
  </div>
</main>

<style>
  .main {
    padding-top: 10%;
    padding-left: 20%;
    padding-right: 7%;
  }

  .profile-layout {
    display: flex;
    justify-content: space-between;
    gap: 2rem; /* Adjust the gap as needed */
  }

  .profile-widget {
    flex: 1; /* Adjust the flex basis as needed */
    max-width: 300px; /* Adjust the width as needed */
  }

  .posts {
    flex: 3; /* Adjust the flex basis as needed */
  }
</style>

<script>
  import Posts from "../../widgets/Posts.svelte";
  import ProfileWidget from "./ProfileWidget.svelte";
  import { onMount } from "svelte";
  import { authToken, refreshToken, isLoginPage, getCurrentUser, server } from "../../stores/stores.js";
  import { navigate } from "svelte-routing"; // Assuming you're using svelte-routing for navigation
  import { get } from "svelte/store";
  import { fetchWithRefresh } from "../../utils/fetchWithRefresh.js";

  let fullName = "";
  let github = "";
  let email = "";
  let userId = 0;

  let isAuthenticated = false;
  
  onMount(async () => {
    isAuthenticated = $authToken !== "";
    console.log($authToken);
    if (!isAuthenticated) {
      $isLoginPage = true;
      navigate("/");
    }
    // get the id from the URL
    const path = window.location.pathname;
    const pathSegments = path.split('/');
    userId = parseInt(pathSegments[pathSegments.length - 1]);  
    console.log(getCurrentUser());  
    console.log(get(authToken));
    console.log(get(refreshToken));
    // if the user is looking at their on profile
    if (userId == getCurrentUser().userId){
      fullName = getCurrentUser().name;
      github = getCurrentUser().github;
      email = getCurrentUser().email;
    } else {
      const profileEndpoint = server + `/api/profile/${userId}`;
      const response = await fetchWithRefresh(profileEndpoint, {
        method: "GET"
      });
      
      if (!response.ok) {
        throw new Error("Failed to fetch profile");
      }
      const data = await response.json();
      fullName = data.full_name;
      github = data.github;
      email = data.email;
    }
    
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
        userId={userId}
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

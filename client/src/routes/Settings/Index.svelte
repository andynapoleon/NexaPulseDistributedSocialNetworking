<script>
    import EditProfileWidget from "./EditProfileWidget.svelte";
    import { onMount } from "svelte";
    import { authToken, isLoginPage, getCurrentUser, server } from "../../stores/stores.js";
    import { navigate } from "svelte-routing"; // Assuming you're using svelte-routing for navigation
  
    let fullName = "";
    let github = "";
    let email = "";
    let userId = 0;
  
    let isAuthenticated = false;
    
    onMount(async () => {
        isAuthenticated = $authToken !== "";
        console.log(isAuthenticated);
        if (!isAuthenticated) {
          $isLoginPage = true;
          navigate("/");
        }
        // get the id from the URL
        userId = getCurrentUser().userId;   
        // if the user is looking at their on profile
        fullName = getCurrentUser().name;
        github = getCurrentUser().github;
        email = getCurrentUser().email;
    });
  </script>
  
  <main class="main">
    <div class="profile-layout">
      <div class="profile-widget">
        <EditProfileWidget
          profileImageUrl="../../../fake_profile.png"
          name={fullName}
          email={email}
          github={github}
        />
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
  </style>
  
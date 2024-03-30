<script>
  // Props passed to the component
  export let profileImage = "https://symprites.com/images/avatars/default.jpg?v=1702987905"; // A default image if none is provided
  export let name = "John Doe";
  export let email = "john.doe@example.com";
</script>

<div class="profile-widget">
  <img class="profile-image" src={profileImage} alt="Profile Avatar" />
  <div class="profile-info">
    <div class="profile-name">{name}</div>
    <div class="profile-email">{email}</div>
  </div>
</div>

<style>
  .profile-widget {
    border: 1px solid #e1e1e1;
    border-radius: 0.5rem;
    padding: 1rem;
    text-align: center;
    width: 350px;
    margin: auto;
    color: black;
  }

  .profile-image {
    display: block;
    width: 6.25rem;
    height: 6.25rem;
    border-radius: 50%;
    margin-bottom: 1rem;
    object-fit: cover;
    margin-left: auto;
    margin-right: auto;
  }

  .profile-info {
    margin-bottom: 0.5rem;
  }

  .profile-name {
    font-size: 1.2em;
    font-weight: bold;
  }

  .profile-email {
    color: #555;
    font-size: 1em;
  }
</style>

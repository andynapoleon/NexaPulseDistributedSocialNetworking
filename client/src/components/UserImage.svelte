<script>
  export let image;
  export let size = "60px"; // default prop value for size
  const baseUrl = process.env.SVELTE_APP_BASE_URL; // URL to get image from the backend
</script>

<div style={`width: ${size}; height: ${size};`}>
  <img
    style="object-fit: cover; border-radius: 50%;"
    width={size}
    height={size}
    alt="user"
    src={`${baseUrl}/assets/${image}`}
  />
</div>

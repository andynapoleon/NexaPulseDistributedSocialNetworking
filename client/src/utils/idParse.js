export function idParse(author) {
    const idComponents = author["id"].split('/'); // Splitting the ID by '/'
    const authorId = idComponents[idComponents.length - 1]; // Extracting the last component
    author["authorId"] = authorId; // Adding the extracted author ID to the author object
    return author; // Returning the extracted author ID
  }
  
export function postIdparse(id){
  const idComponents = id.split('/');
  const postId = idComponents[idComponents.length - 1];
  const authorId = idComponents[idComponents.length - 3];
  return {postId, authorId};
}
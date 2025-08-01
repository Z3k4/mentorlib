export function getInitialLetter(user) {
    return user.first_name.slice(0,1).toUpperCase() + user.last_name.slice(0,1).toUpperCase() || "UU"
}
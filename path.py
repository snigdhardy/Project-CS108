def is_valid_move(grid, visited, row, col):
    rows = len(grid)
    cols = len(grid[0])
    return (1 <= row < rows - 1) and (1 <= col < cols - 1) and (grid[row][col] == '0') and not visited[row][col]

def dfs(grid, visited, row, col, path):
    if row == len(grid) - 2 and col == len(grid[0]) - 2:
        return True
    
    if is_valid_move(grid, visited, row, col):
        visited[row][col] = True

        # Check right
        if dfs(grid, visited, row, col + 1, path):
            path.append('R')
            return True

        # Check down
        if dfs(grid, visited, row + 1, col, path):
            path.append('D')
            return True

        # Check left
        if dfs(grid, visited, row, col - 1, path):
            path.append('L')
            return True

        # Check up
        if dfs(grid, visited, row - 1, col, path):
            path.append('U')
            return True

        return False

def find_path(grid):
    if not grid:
        return []
    
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path = []
    
    if dfs(grid, visited, 1, 1, path):
        return path[::-1]  # Reverse the path since it's built backwards
    else:
        return []
from utils import rc2g
class DLXNode:
    def __init__(self,left=None,right=None,up=None,down=None,col=None,id=None):
        self.left = left or self
        self.right = right or self
        self.up = up or self
        self.down = down or self
        self.col = col or self
        self.id = id
    
    def insert_right(self,node):
        node.left = self
        node.right = self.right
        self.right.left = node
        self.right = node
        pass

    def insert_down(self,node):
        node.up = self
        node.down = self.down
        self.down.up = node
        self.down = node
        pass
    
    def remove_col(self):
        cur = self
        while True:
            cur.left.right = cur.right
            cur.right.left = cur.left
            cur = cur.down
            if cur == self: break
        pass
    def recover_col(self):
        cur = self
        while True:
            cur.left.right = cur
            cur.right.left = cur
            cur = cur.down
            if cur == self: break
        pass    
    def remove_row(self):
        cur = self
        while True:
            cur.up.down = cur.down
            cur.down.up = cur.up
            cur = cur.right
            if cur == self: break
        pass
    def recover_row(self):
        cur = self
        while True:
            cur.up.down = cur
            cur.down.up = cur
            cur = cur.right
            if cur == self: break
        pass    

class DLXMap:
    def get_cols(self,r,c,v):
        exist = r*9 + c
        row = 81 + r*9 + (v-1)
        col = 81*2 + c*9 + (v-1)
        grid = 81*3 + rc2g(r,c)*9 + (v-1)
        return exist,row,col,grid

    def add_row(self,r,c,v):
        if v == 0:
            for i in range(1,10):
                self.add_row(r,c,i)
        else:

            cols = self.get_cols(r,c,v)
            nodes = []
            for col in cols:
                nodes.append(DLXNode(col=self.c[col],id=(r,c,v)))
                self.c[col].insert_down(nodes[-1])
            for i in range(3):
                nodes[i].insert_right(nodes[i+1])
        pass

    def del_conflict_row(self,r,c,v):
        if v != 0:
            cols = self.get_cols(r,c,v)
            ids = [self.c[x].id for x in cols]
            #print(ids)
            for col in cols:
                cur = self.c[col]
                cur.remove_col()
                while True:
                    cur = cur.down
                    if cur == self.c[col]: break
                    if cur.right != cur:
                        cur.right.remove_row()
        pass

    def update(self,id,inv=False):
        r,c,v = id
        self.mat[r][c] = -v
        if inv:
            self.mat[r][c] = 0
        #if inv:
        #    print(f'remove{id}')
        #else:
        #    print(f'add{id}')
                    
    def display(self):
        print(self.mat)

        
                
    def __init__(self,mat):
        self.mat = mat
        self.head = DLXNode()
        self.c = []
        self.stack = []
        self.ans = []

        for i in range(324):
            self.c.append(DLXNode(id=323-i))
        for i in range(324):
            self.head.insert_right(self.c[i])

        for i in range(9):
            for j in range(9):
                if mat[i][j] == 0:
                    self.add_row(i,j,mat[i][j])
        for i in range(9):
            for j in range(9): 
                self.del_conflict_row(i,j,mat[i][j])  

    def solve(self):
        #print(f'======solve======{len(self.stack)}')
        if self.head.right == self.head:
            return True
        node = self.head.right
        while node != self.head:
            if node.down == node:
                #print('==Track Back==')
                return False
            node = node.right

        #remove stem col + row
        first_col = self.head.right
        first_col.remove_col()
        self.stack.append(first_col.recover_col)
        cur_row = first_col.down
        while cur_row != first_col:
            if cur_row.right != cur_row:
                cur_row.right.remove_row()
                self.stack.append(cur_row.right.recover_row)
            cur_row = cur_row.down
        #print(f'*******del col&row above********')    
        cur_depth = len(self.stack)
        select_row = first_col.down
        #enumerate select row in first col
        while select_row != first_col:
            self.update(select_row.id)
            if select_row.right != select_row:
                cur_col = select_row.right
                # delete all related cols in select row
                while True:
                    col_node = cur_col.col
                    col_node.remove_col()
                    self.stack.append(col_node.recover_col)
                    col_node = col_node.down
                    #delete rows in the deleted cols
                    while col_node != col_node.col:
                        if col_node.right != col_node:
                            col_node.right.remove_row()
                            self.stack.append(col_node.right.recover_row)
                        col_node = col_node.down
                    cur_col = cur_col.right
                    if cur_col == select_row.right: break
                if self.solve():
                    return True
            self.update(select_row.id,inv=True)
            while len(self.stack) > cur_depth:self.stack.pop()()
            select_row = select_row.down
        return False
        
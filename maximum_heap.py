from functools import total_ordering
import math
class Max_heap():
    def __init__(self):
        #inicia com o heap com um elemento sentinela (que nunca será acessado)
        self.arr_heap = [None] # vector representation 

    def __str__(self):
        return str(self.arr_heap[1:])

    def __repr__(self):
        return str(self)
    
    #Os metodos esquerda, direita e pai serão usados nos demais metodos do heap
    def left(self, i:int) ->int:
        """
            Retorna a posição do filho a esquerda de i
        """
        return 2*i

    def right(self, i:int) ->int:
        """
            Retorna a posição do filho a direita de i
        """
        return 2*i+1

    def parent(self, i:int) ->int:
        """
        Retorna a posição do pai do i-ésimo nó
        """
        return math.ceil((i-1)/2)
    
    @property
    def last_item_index(self) -> int:
        return len(self.arr_heap)-1

    @property
    def peek_root(self) -> int:
        return self.arr_heap[1]

    def print_heap(self,i=1,tab=""):
        if(i<len(self.arr_heap)-1):
            print(f"[{i}]:{tab}{self.arr_heap[i]}")
            self.print_heap(self.left(i),tab+"|    ")
            self.print_heap(self.right(i),tab+"|    ")

    # called internally
    def restructure(self, pos_raiz_sub_arvore:int):
        #maior_filho é inicializado com o da esqueda de pos raiz subarvore
        pos_pai = pos_raiz_sub_arvore
        pos_maior_filho = self.left(pos_pai)
        #obtem o item raiz da subarvore do heap
        val_raiz_sub_arvore = self.arr_heap[pos_raiz_sub_arvore]
        while pos_maior_filho <=self.last_item_index:
            #se a posição do filho a esquerda não for a ultima do vetor,
            #atualize, se necessario, o pos_maior_filho considerando o filho a direita
            if pos_maior_filho<self.last_item_index:
                if self.arr_heap[pos_maior_filho]<self.arr_heap[self.right(pos_pai)]:
                    pos_maior_filho=self.right(pos_pai)
            #caso o valor da  raiz desta subarvore (val_raiz_sub_arvore)
            #possua um valor maior que o de seus filhos, 
            # finaliza o while 
            if (val_raiz_sub_arvore > self.arr_heap[pos_maior_filho]):
                break#ou apenas self.arr_heap[pos_maior_filho]
            #realize a troca conforme especificação
            self.arr_heap[pos_pai] = self.arr_heap[pos_maior_filho]
            #prepare as variáveis pos_pai e pos_maior_filho para a proxima iteração
            pos_pai = pos_maior_filho
            pos_maior_filho = self.left(pos_maior_filho)
        #atualize a posição pos_pai apropriadamente
        self.arr_heap[pos_pai] = val_raiz_sub_arvore
    def pop_max(self):
        el_maximoo=0
        if len(self.arr_heap)<=1:
            return None
           #raise IndexError("Heap Vazio")
        else:
            #print("our list:",self.arr_heap)
            el_maximoo = self.arr_heap[1]
            #print(f"first is el_maximoo:{self.arr_heap[1]}=={el_maximoo}==1")
            self.arr_heap[1] = self.arr_heap[len(self.arr_heap)-1]
            #print(f"first recieves {self.arr_heap[len(self.arr_heap)-1]} from {self.arr_heap} in last pos {len(self.arr_heap)-1} ")
            self.arr_heap.pop()
            
            #print("final size:",len(self.arr_heap))
            if len(self.arr_heap)<=1:
                return el_maximoo
            else:
                self.restructure(1)
        return el_maximoo
    def insert(self, item):
        self.arr_heap.append(item)
        pos_inserir = self.last_item_index
        pai_pos_inserir = self.parent(pos_inserir)
        #print(f"pi {pos_inserir}:{self.arr_heap[pos_inserir]} ppi {pai_pos_inserir}:{self.arr_heap[pai_pos_inserir]}")
        while pos_inserir>1 and self.arr_heap[pos_inserir]>self.arr_heap[pai_pos_inserir]:
            #print(f"{self.arr_heap[pos_inserir]}>{self.arr_heap[pai_pos_inserir]}")
            #realiza a atualização
            swap_aux = self.arr_heap[pai_pos_inserir] 
            self.arr_heap[pai_pos_inserir] = self.arr_heap[pos_inserir]
            self.arr_heap[pos_inserir] = swap_aux
            #print(f"updated arr_heap[pai_pos_inserir] to {self.arr_heap[pai_pos_inserir]}")
            pos_inserir = pai_pos_inserir
            pai_pos_inserir = self.parent(pos_inserir)
            #print(f"next it> pi {pos_inserir}:{self.arr_heap[pos_inserir]} ppi {pai_pos_inserir}:{self.arr_heap[pai_pos_inserir]}")
        #finalizando o insere
        self.arr_heap[pos_inserir]=item
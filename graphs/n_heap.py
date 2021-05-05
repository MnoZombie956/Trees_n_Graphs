from functools import total_ordering
import math
class MinHeap:

    def __init__(self):
        #inicia com o heap com um elemento sentinela (que nunca será acessado)
        self.arr_heap = [None]

    def __str__(self):
        return str(self.arr_heap[1:])

    def __repr__(self):
        return str(self)
        
    def esquerda(self, i:int) ->int:
        """
            Retorna a posição do filho a esquerda de i
        """
        return 2*i

    def direita(self, i:int) ->int:
        """
            Retorna a posição do filho a direita de i
        """
        return 2*i+1

    def pai(self, i) ->int:
        """
            Retorna a posição do pai do i-ésimo nó
        """
        return math.floor(i/2)

    @property
    def pos_ultimo_item(self):
        return len(self.arr_heap)-1

    def refaz(self, pos_raiz_sub_arvore:int):
         #maior_filho é inicializado com o da esqueda de pos raiz subarvore
        pos_pai = pos_raiz_sub_arvore
        pos_menor_filho = self.esquerda(pos_pai)


        #obtem o item raiz da subarvore do heap
        val_raiz_sub_arvore = self.arr_heap[pos_raiz_sub_arvore]


        while pos_menor_filho <=self.pos_ultimo_item:
            #se a posição do filho a esquerda não for a ultima do vetor,
            #atualize, se necessario, o pos_menor_filho considerando o filho a direita
            if pos_menor_filho<self.pos_ultimo_item:
                #### SEU CODIGO AQUI ############
                if self.arr_heap[pos_menor_filho]>self.arr_heap[self.direita(pos_pai)]:
                    pos_menor_filho=self.direita(pos_pai)

            #caso o valor da  raiz desta subarvore (val_raiz_sub_arvore)
            #possua um valor maior que o de seus filhos, 
            # finaliza o while 
            #### SEU CODIGO AQUI ############

            if (val_raiz_sub_arvore < self.arr_heap[pos_menor_filho]):
                break#ou apenas self.arr_heap[pos_menor_filho]

            #realize a troca conforme especificação
            #### SEU CODIGO AQUI ############

            self.arr_heap[pos_pai] = self.arr_heap[pos_menor_filho]

            #prepare as variáveis pos_pai e pos_menor_filho para a proxima iteração
            #substitua os "None" das duas linhas abaixo apropriadamente
            pos_pai = pos_menor_filho
            pos_menor_filho = self.esquerda(pos_pai)

        #atualize a posição pos_pai apropriadamente
        self.arr_heap[pos_pai] = val_raiz_sub_arvore

    def insere(self,item):
        self.arr_heap.append(item)

        pos_inserir = self.pos_ultimo_item
        pai_pos_inserir = self.pai(pos_inserir)

        #print(f"pi {pos_inserir}:{self.arr_heap[pos_inserir]} ppi {pai_pos_inserir}:{self.arr_heap[pai_pos_inserir]}")
        #substitua o "None" apropriadamente
        while pos_inserir>1 and self.arr_heap[pos_inserir]<self.arr_heap[pai_pos_inserir]:
            #print(f"{self.arr_heap[pos_inserir]}>{self.arr_heap[pai_pos_inserir]}")
            #realiza a atualização (substitua os "None")
            swap_aux = self.arr_heap[pai_pos_inserir] 
            self.arr_heap[pai_pos_inserir] = self.arr_heap[pos_inserir]
            self.arr_heap[pos_inserir] = swap_aux
            #print(f"updated arr_heap[pai_pos_inserir] to {self.arr_heap[pai_pos_inserir]}")

            #ajusta para a proxima iteração (substitua os None apropriadamente)
            pos_inserir = pai_pos_inserir
            pai_pos_inserir = self.pai(pos_inserir)
            #print(f"next it> pi {pos_inserir}:{self.arr_heap[pos_inserir]} ppi {pai_pos_inserir}:{self.arr_heap[pai_pos_inserir]}")

        #finalize o insere apropriadamente
        self.arr_heap[pos_inserir]=item

    def retira_min(self):
        el_minimoo=0
        if len(self.arr_heap)<=1:
            return None
           #raise IndexError("Heap Vazio")
        else:
            #print("our list:",self.arr_heap)
            el_minimoo = self.arr_heap[1]
            #print(f"first is el_minimoo:{self.arr_heap[1]}=={el_minimoo}==1")
            self.arr_heap[1] = self.arr_heap[len(self.arr_heap)-1]
            #print(f"first recieves {self.arr_heap[len(self.arr_heap)-1]} from {self.arr_heap} in last pos {len(self.arr_heap)-1} ")
            self.arr_heap.pop()
            
            #print("final size:",len(self.arr_heap))
            if len(self.arr_heap)<=1:
                return el_minimoo
            else:
                self.refaz(1)

        return el_minimoo
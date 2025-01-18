section .bss
    t3 resd 1
    y resd 1
    x resd 1
    t0 resd 1
section .data
msg0: db "dentro do if", 0xA, 0
msg1: db "dentro de nv", 0xA, 0
msg2: db "IF", 0xA, 0
msg3: db "Else", 0xA, 0
section .text
    global _start

_start:
    mov dword [x], 0
    mov dword [y], 0
    mov dword [x], 0
    mov dword [y], 3
    mov eax, 6
    cmp eax, 3
    jg L1
    jmp L2
L1:
    mov eax, [x]
    cmp eax, 4
    jl L4
    jmp L5
L4:
    mov dword [x], 5
    mov eax, 1
    mov edi, 1
    mov esi, msg0
    mov edx, 14
    syscall
    mov eax, 1
    mov edi, 1
    mov esi, msg1
    mov edx, 14
    syscall
    jmp L5
L5:
    mov dword [x], 6
    mov eax, 1
    mov edi, 1
    mov esi, msg2
    mov edx, 4
    syscall
    jmp L6
L2:
    mov dword [x], 0
    mov eax, 1
    mov edi, 1
    mov esi, msg3
    mov edx, 6
    syscall
    jmp L6
L6:
    mov dword [x], 2
    mov eax, 60
    xor edi, edi
    syscall

print_int:
    ; Converte o número inteiro em string e imprime
    push edi
    push esi
    push edx

    mov esi, esp             ; Ponteiro para a string (stack)
    mov ecx, 10              ; Base decimal
    xor edx, edx

print_loop:
    xor edx, edx             ; Limpa edx
    div ecx                  ; Divide eax por 10
    add dl, '0'              ; Converte dígito para caractere
    dec esi                  ; Move ponteiro para trás
    mov [esi], dl            ; Armazena dígito na string
    test eax, eax            ; Verifica se ainda há dígitos
    jnz print_loop

    mov edx, esp             ; Ponteiro para a string
    mov eax, 1               ; syscall: write
    mov edi, 1               ; stdout
    sub edx, esi             ; Tamanho da string
    syscall

    pop edx
    pop esi
    pop edi
    ret

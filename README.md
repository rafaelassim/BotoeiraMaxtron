# BotoeiraMaxtron

Dependências:
    pyserial


    def pedido_viateclado():
    global region_tot
    global region_nome

    global maquinas_nome
    global maquinas_tot
    global keyboard_msg
    
    global produto_tot  
    global produtos_bitola

    global produtos_bitola_tot 
    global produtos_bitola_nomes 

    pointer = 0
    regiao_selecionada = pointer
    maquina_selecionada = 0
    
    bitola_selecionada = 0
    subproduto_selecionado = 0
    print ("Processo teclado")
    main_menu.clear_display()
    time.sleep(0.1)
    main_menu.write_line1('Sel.Reg:')
    main_menu.write_line2(maquinas_nome[pointer])

    while True:
        maquina_selecionada= processo_selecao(regiao_selecionada,region_tot,region_nome)
        if keyboard_msg=='ENT':
            keyboard_msg=''
            main_menu.clear_display()
            time.sleep(0.1)
            print("Regiao Selecionada: ",maquinas_nome[maquina_selecionada])
            main_menu.write_line1('Sel.Bito')
            main_menu.write_line2(produtos_bitola[bitola_selecionada])
            while True:
                bitola_selecionada= processo_selecao(bitola_selecionada,produto_tot,produtos_bitola)
                time.sleep(0.250)
                if keyboard_msg=='ENT':
                   produtos_bitola_nomes=datareader.produto_bitola_items(produtos_bitola[bitola_selecionada])
                   produtos_bitola_tot=len(produtos_bitola_nomes)
                   print("Bitola selecionada ", produtos_bitola[bitola_selecionada])

                   main_menu.write_line1('SubProd.')
                   main_menu.write_line2(produtos_bitola_nomes[0])

                   keyboard_msg='keyboard_msg'
                   while True:
                        subproduto_selecionado= processo_selecao(subproduto_selecionado,produtos_bitola_tot,produtos_bitola_nomes)
                        time.sleep(0.250)
                        if keyboard_msg=='ENT':
                            print("SubProduto Selecionado ", produtos_bitola_nomes[subproduto_selecionado])
                            print("selecionado maquina, bitola e subproduto")
                            enviar_command(datareader.tag_machines(maquinas_nome[maquina_selecionada]),datareader.tag_produto(produtos_bitola[bitola_selecionada],produtos_bitola_nomes[subproduto_selecionado]))
                            return
                        if keyboard_msg =='CLR':
                            break
                if keyboard_msg =='CLR':
                    break
            #pointer= processo_selecao(pointer,maquinas_tot,maquinas_nome)
            if keyboard_msg =='CLR':
                break
        
        if keyboard_msg =='CLR':
            break
        time.sleep(0.250)
    return
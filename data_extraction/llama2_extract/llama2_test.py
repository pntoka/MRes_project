import llama2_extract as le

if __name__ == '__main__':
    # paras = [
    #     "CQDs were synthesized by the usage of O. basilicum L. extract via a simple hydrothermal method (Fig. 1). In a typical one-step synthesizing procedure, 2.0 g of O. basilicum L. seed was added to 100 mL of distilled water and stirred at 50 °C for 2 h. Then, the obtained extract was filtered and transferred into a 100 mL Teflon-lined stainless-steel autoclave to be heated at 180 °C for 4 h. Once the autoclave was cooled naturally at room temperature and the solution was centrifuged (12,000 rpm) for 15 min, the prepared brown solution was filtered through a fine-grained 0.45 μm membrane to remove larger particles. Finally, the solution was freeze-dried to attain the dark brown powder of CQDs.",
    #     "S-doped C-dots were synthesized using a hydrothermal method. Briefly, 25 mL sodium citrate solution (0.1 M) and sodium thiosulfate were added into a 50 mL Teflon-lined stainless steel autoclave. After that, the autoclave was kept at a fixed temperature (160, 180, 200, 220 or 240 °C) for 6 h. The product could be used after filtration with a cylinder filtration membrane filter (0.22 μm)."
    # ]
    # for para in paras:
    #     result = le.llama_time_extract(para)
    #     print(result)
    file_dir = '/home/ptoka/para_30_sample.txt'
    save_dir = '/home/ptoka/llama_time_temp_30_sample.json'
    output = le.llama_temp_time_extract(file_dir, save_dir)
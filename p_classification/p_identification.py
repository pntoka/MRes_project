import pidentifier as pid

if __name__ == '__main__':
    batch_no = list(range(11,29))
    for batch in batch_no:
        path = f'/home/ptoka/article_json/batch_no_{batch}_json'
        save_dir = '/home/ptoka/paras_id'
        results = pid.get_synthesis_methods(path)
        pid.write_paragraphs_df_to_txt(results,save_dir, f'batch_{batch}_paras.txt')
import os
import random
import dotenv


class pronouns_page_api():
    terms_cookies = {
        '_csrf': 'aSk3LqUzgAAZGQsOBDUClIRv',
        'token': os.getenv("ppToken"),
    }

    terms_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://en.pronouns.page/api',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    }

class cgpt_api():    
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Api-Key': os.getenv("cptToken"),
    'Content-Type': 'multipart/form-data; boundary=---------------------------14582556183550688363729607185',
    'Origin': 'https://deepai.org',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}
    
mjheaders = {
   #  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://stablediffusion.gigantic.work/',
    'Content-Type': 'application/json',
   #  'Origin': 'https://stablediffusion.gigantic.work',
   #  'Alt-Used': 'stablediffusion.gigantic.work',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin'
}


mjjson_data = { 'prompt': '%s',
    'seed': 2521705115,
    'used_random_seed': True,
    'negative_prompt': '',
    'num_outputs': 1,
    'num_inference_steps': 25,
    'guidance_scale': 7.5,
    'width': 1024,
    'height': 1024,
    'vram_usage_level': 'balanced',
    'sampler_name': 'dpmpp_2m',
    'use_stable_diffusion_model': 'sd_xl_base_1.0',
    'clip_skip': False,
    'use_vae_model': 'sdxl_vae',
    'stream_progress_updates': True,
    'stream_image_progress': False,
    'show_only_filtered_image': True,
    'block_nsfw': True,
    'output_format': 'jpeg',
    'output_quality': 75,
    'output_lossless': False,
    'metadata_output_format': 'json',
    'original_prompt': '%s',
    'active_tags': [],
    'inactive_tags': [],
    'save_to_disk_path': '/data/easy-diffusion-images',
    'use_face_correction': 'GFPGANv1.4',
    'session_id': '1698108672042',}


ssearch_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.chosic.com/',
    'Authorization': os.getenv("spotifyToken"),
    'Content-Type': 'application/json',
    'Origin': 'https://www.chosic.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

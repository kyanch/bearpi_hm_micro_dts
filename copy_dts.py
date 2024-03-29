import os
import re
import shutil
import sys

def copy_includes(target_path:str,file_name:str,search_paths:list[str],copied_files:list[str]):
	"""
	递归复制dts和它的#include。
	"""
		
	if file_name in copied_files:
		return
    
	copied_files.add(file_name)
    
	for search_path in search_paths:
		src_path = os.path.join(search_path,file_name)
		if os.path.isfile(src_path):
			dst_path = os.path.join(target_path,file_name)
			os.makedirs(os.path.dirname(dst_path),exist_ok=True)
			shutil.copy(src_path,dst_path)
			print(f"Copy: {src_path} -> {dst_path}")
            
			with open(src_path,'r') as f:
				content = f.read()
				includes = re.findall(r'#include\s*["<](.*?)[">]',content)
				for inc in includes:
					copy_includes(target_path,inc,search_paths,copied_files)
     
			break
	else:
			print(f"Warning: file not found {file_name}")

def main(target_path,dts_file_name,uboot_path):
	if not dts_file_name or not uboot_path:
		print("Usage: python copy_dts.py <file_name> <u-boot-repo-path>")
		sys.exit(1)
  
	search_paths=[os.path.join(uboot_path,sub_dir) for sub_dir in ['arch/arm/dts', 'include']]
	copied_files = set()
	copy_includes(target_path,dts_file_name,search_paths,copied_files)

if __name__ =="__main__":
	if len(sys.argv)!=4:
		print("Usage: python copy_dts.py <dts_name> <target_path> <uboot_path>")
		sys.exit(1)
	main(sys.argv[2],sys.argv[1],sys.argv[3])
	
            
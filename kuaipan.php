#!/usr/bin/php -q
<?php
	date_default_timezone_set('Asia/Shanghai');
	
	$data = array(
				array(
					'username' => '用户名',
					'password' => ''
				),	
			);
	echo '***************'.date('Y-m-d').'*********************'.chr(10);

	foreach( $data as $user ){
		op($user['username'],$user['password'])	;
	}
	echo chr(10);
	echo chr(10);
	echo chr(10);
	echo chr(10);

	function op ($username,$password){
		$url = 'https://www.kuaipan.cn/index.php?ac=account&op=login'; 
		$pre_url = 'https://www.kuaipan.cn/account_login.htm';
		$cookiejar = tempnam('tmp','cookie');
		$handle = curl_init();
		curl_setopt($handle,CURLOPT_COOKIEJAR,$cookiejar);
		curl_setopt($handle,CURLOPT_URL,$pre_url);
		curl_setopt($handle, CURLOPT_RETURNTRANSFER, 1);
		curl_exec($handle);
		curl_close($handle);
		


		/**
		 * 登录
		 **/
		$handle = curl_init();
		curl_setopt($handle,CURLOPT_URL,$url);
		curl_setopt($handle,CURLOPT_POSTFIELDS,"username=$username&userpwd=$password&isajax=yes");
		curl_setopt($handle, CURLOPT_RETURNTRANSFER, 1);
		$header = array();
		$header[] = 'X-Requested-With:XMLHttpRequest';

		curl_setopt($handle,CURLOPT_HTTPHEADER,$header);
		//curl_setopt($handle,CURLOPT_HEADER,1);
		curl_setopt($handle,CURLOPT_COOKIEFILE,$cookiejar);
		$cookiejar2 = tempnam('tmp','cookie'); 
		curl_setopt($handle,CURLOPT_COOKIEJAR,$cookiejar2);
		$result = curl_exec($handle);
		curl_close($handle);

		$result = json_decode($result);
		if( $result->errcode =='ok' ){
			echo $username.' 登录成功'.chr(10);
		}else{
			echo '登录失败，签到未成功！'.chr(10); return ; }
		
		$signurl = 'http://www.kuaipan.cn/index.php?ac=common&op=usersign';
		$handle = curl_init();
		curl_setopt($handle,CURLOPT_URL,$signurl);
		curl_setopt($handle, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($handle,CURLOPT_COOKIEFILE,$cookiejar2);
		$r = curl_exec($handle);
		curl_close($handle);
		$r = json_decode($r,true);
		if( !is_array( $r ) ){
			echo '出了点错，hwz';	
			return ;
		}
		if( $r['state'] == '-102' ){
			echo '已签到过!'.chr(10);
			return ;
		}
		echo "签到成功，{$r['status']['points']}积分，{$r['rewardsize']}M永久空间到手！".chr(10);
		echo chr(10);
		return ;
	}



//end of file 


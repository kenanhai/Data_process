#include <VIPLFaceDetector.h>
#include <VIPLPointDetector.h>
#include <VIPLFaceRecognizer.h>

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <memory>
#include <iostream>
#include <string>
#include<fstream>

const VIPLImageData vipl_convert(const cv::Mat &img)
{
	VIPLImageData vimg(img.cols, img.rows, img.channels());
	vimg.data = img.data;
	return vimg;
}

static std::shared_ptr<float> ExtractFeature(VIPLFaceDetector &FD, VIPLPointDetector &PD, VIPLFaceRecognizer &FR, const VIPLImageData &image)
{
	// 进行人脸检测
	std::vector<VIPLFaceInfo> infos = FD.Detect(image);
	std::shared_ptr<float> feats(new float[FR.GetFeatureSize()], std::default_delete<float[]>());
	auto feats_length = FR.GetFeatureSize();
	if (infos.size() > 0)
	{
		int i = 0;
		VIPLPoint5 points;
		PD.DetectLandmarks(image, infos[i], points);
		FR.ExtractFeatureWithCrop(image, points, feats.get());
	}
	else
	{
		for (int i = 0; i < feats_length; ++i) feats.get()[i] = 0;
	}
	return feats;
}

static std::shared_ptr<float> ExtractFeature(VIPLFaceDetector &FD, VIPLPointDetector &PD, VIPLFaceRecognizer &FR, const std::string &path)
{
	// 加载图片
	cv::Mat mat = cv::imread(path, cv::IMREAD_COLOR);  // Bitmap for BGR layout
	auto image = vipl_convert(mat);

	return ExtractFeature(FD, PD, FR, image);
}

#define M 6580
#define N 6580

int main()
{

	VIPLFaceDetector FD("D:/programs/Seetatech/model/VIPLFaceDetector5.1.2.m9d6.640x480.sta", VIPLFaceDetector::CPU);
	VIPLPointDetector PD("D:/programs/Seetatech/model/VIPLPointDetector5.0.pts5.dat");
	VIPLFaceRecognizer FR("D:/programs/Seetatech/model/VIPLFaceRecognizer5.0.RN50.32w.s4.ID.sta", VIPLFaceRecognizer::CPU);//VIPLFaceRecognizer5.0.RN50.32w.s4.ID.sta   VIPLFaceRecognizer5.0.RN50.49w.s4.1N.sta

	FD.SetMinFaceSize(40); //设置最小检测人脸
	//输出分数记录
	std::string nameStr01 = "D:\\programs\\Seetatech\\log.txt";
	std::string nameStr02 = "D:\\programs\\Seetatech\\log_mat.txt";
	std::ofstream outfile01(nameStr01);
	std::ofstream outfile02(nameStr02);

	//指定测试集txt
	std::ifstream in01("D:\\programs\\Seetatech\\txt\\src-6580.txt");
	std::ifstream in02("D:\\programs\\Seetatech\\txt\\id-6580.txt");

	for (int i = 0; i <1; i++)
	{
		std::string line01 = "", line02 = "";
		std::string str01[M], str02[N];
		int k1 = 0,k2 = 0;
		//float *a1[M], *a2[M];
		//if (in01)
			//getline(in01, line01);
		//if (in02)
			//getline(in02, line02);
		
		///*
		std::vector<std::shared_ptr<float>>a1(M);
		std::vector<std::shared_ptr<float>>a2(N);
		while (getline(in01, line01))
		{
			//auto feats1 = ExtractFeature(FD, PD, FR, line01);
			//a1[k1] = feats1.get();
			std::cout << line01 << std::endl;
			for (int h1 = 0; h1 < 1; h1++)
			{			
			a1[k1] = ExtractFeature(FD, PD, FR, line01);
			continue;
			}			
			str01[k1] = line01;
			k1++;
		}
		while (getline(in02, line02))
		{
			std::cout << line02 << std::endl;
			for (int h2 = 0; h2 < 1; h2++)
			{			
			a2[k2] = ExtractFeature(FD, PD, FR, line02);
			continue;
			}			
			str02[k2] = line02;
			k2++;
		}
		//*/
		/*
		std::cout << "The first picture:" << line01<<std::endl;
		std::cout << "The second picture:" << line02 << std::endl;	
		auto feats1 = ExtractFeature(FD, PD, FR, line01);//argv[1]
		auto feats2 = ExtractFeature(FD, PD, FR, line02);//argv[2]
		std::cout << typeid(feats1).name() << std::endl;
		std::cout << typeid(feats1.get()).name() << std::endl;
		std::cout << feats1.get() << std::endl;
		std::cout << *feats1.get()<<std::endl;
		*/
		//float similar = FR.CalcSimilarity(feats1.get(), feats2.get());

		float similar;
		for (int m1 = 0; m1<M; m1++)
		{
			outfile01 << str01[m1] << std::endl;
			for (int m2 = 0; m2<N; m2++)
			{	
				similar = 0;
				similar = FR.CalcSimilarity(a1[m1].get(), a2[m2].get());
				outfile02 << similar << " ";
				if (similar > 0.7)
				{
					outfile01 << str02[m2] << " " << "Similarity: " << similar <<std::endl;
				}
				std::cout << "Similarity: " << similar << std::endl << std::endl;				
			}
			outfile01 << std::endl;
			outfile02 << std::endl;
		}
	}
	in01.close();
	in02.close();
	return 0;
}
